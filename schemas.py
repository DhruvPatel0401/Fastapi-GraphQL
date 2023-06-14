import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from db_conf import db_session
import models

app = FastAPI()

class PostSchema(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostSchema)

    def resolve_all_posts(self, info):
        query = models.Post.query.all()
        return query


class CreateNewPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, title, content):
        db_post = models.Post(title=title, content=content)
        db_session.add(db_post)
        db_session.commit()
        db_session.refresh(db_post)
        ok = True
        return CreateNewPost(ok=ok)


class Mutation(graphene.ObjectType):
    create_new_post = CreateNewPost.Field()


app.mount("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation), on_get=make_graphiql_handler()))
