import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp

app = FastAPI()

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema()))