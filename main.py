import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from schemas import PostSchema
from db_conf import db_session
import models

app = FastAPI()

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostSchema)

    def resolve_all_post(self, info):
        query = models.Post.query.all()
        return query


class CreateNewPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, title, content):
        post = PostSchema(title=title, content=content)
        db_post = models.Post(title=post.title, content=post.content)
        db_session.add(db_post)
        db_session.commit()
        db_session.refresh(db_post)
        ok = True
        return CreateNewPost(ok=ok)


class PostMutations(graphene.ObjectType):
    create_new_post = CreateNewPost.Field()


app.mount("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=PostMutations), on_get=make_graphiql_handler()))
