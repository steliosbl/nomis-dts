using GraphQL.Types;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Core.Helpers;
using Nomis.Interfaces.Contacts.Repository;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Variables.Repository;

using fe_api.GraphQL.Types;

namespace fe_api.GraphQL {
    public class NomisQuery : ObjectGraphType<object> {
        public NomisQuery(IContactStore contacts, IDatasetStore datasets, IVariableStore variables) {
            Name = "Query";

            Field<ContactType>(
                name: "contact",
                description: "Obtain information about a particular contact.",
                arguments: new QueryArguments(new QueryArgument<NonNullGraphType<StringGraphType>> { Name = "id" }),
                resolve: context => contacts.GetAsync(context.Arguments["id"].ToString())
            );

            Field<ListGraphType<ContactType>>(
                name: "contacts",
                description: "List all contacts.",
                resolve: context => contacts.GetAsync(null)
            );

            Field<DatasetType>(
                name: "dataset",
                description: "Obtain information about a particular dataset.",
                arguments: new QueryArguments(new QueryArgument<NonNullGraphType<StringGraphType>> { Name = "id" }),
                resolve: context => datasets.GetAsync(context.Arguments["id"].ToString())
            );

            QueryArguments datasetArgs = new QueryArguments();
            datasetArgs.Add(new QueryArgument<StringGraphType> { Name = "id", Description = "Search by ID of dataset." });
            datasetArgs.Add(new QueryArgument<StringGraphType> { Name = "title", Description = "Search by title." });

            Field<ListGraphType<DatasetType>>(
                name: "datasets",
                description: "List all datasets.",
                arguments: datasetArgs,
                resolve: context => {
                    QueryFilterOptions options = new QueryFilterOptions();
                    options.Query.Value = Lucene.BuildQuery(context.Arguments);
                    options.Query.Syntax = Syntax.Lucene;
                    return datasets.GetAllAsync(options);
                }
            );

            Field<VariableType>(
                name: "variable",
                description: "Obtain information about a variable.",
                arguments: new QueryArguments(
                    new QueryArgument<NonNullGraphType<StringGraphType>> { Name = "name" },
                    new QueryArgument<StringGraphType> { Name = "view" }
                ),
                resolve: context => variables.GetAsync(
                    context.Arguments["name"].ToString(),
                    (context.Arguments.ContainsKey("view"))? context.Arguments["view"].ToString() : null)
            );

            QueryArguments variableArgs = new QueryArguments();
            variableArgs.Add(new QueryArgument<StringGraphType> { Name = "name", Description = "Search by name." });
            variableArgs.Add(new QueryArgument<StringGraphType> { Name = "label", Description = "Search by title." });
            
            Field<ListGraphType<VariableType>>(
                name: "variables",
                description: "List all variables.",
                arguments: datasetArgs,
                resolve: context => {
                    QueryFilterOptions options = new QueryFilterOptions();
                    options.Query.Value = Lucene.BuildQuery(context.Arguments);
                    options.Query.Syntax = Syntax.Lucene;
                    return variables.GetAllAsync(options);
                }
            );
        }
    }
}