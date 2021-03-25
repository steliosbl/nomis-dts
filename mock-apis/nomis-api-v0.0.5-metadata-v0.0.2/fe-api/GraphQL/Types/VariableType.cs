using GraphQL.Types;

using Nomis.Interfaces.Core.Helpers;
using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Variables.Models;
using Nomis.Interfaces.Variables.Repository;

namespace fe_api.GraphQL.Types {
    public class VariableType : ObjectGraphType<Variable> {
        public VariableType(ICategoryStore categories, ICategoryTypeStore categoryTypes) {
            Field(x => x.Name).Description("Unique name.");
            Field(x => x.Label, nullable: true).Description("Label for display purposes.");
            Field(
                name: "defaults",
                description: "Default selections of categories.",
                type: typeof(ListGraphType<StringGraphType>),
                resolve: x => x.Source.Defaults
            );


            QueryArguments categoryArgs = new QueryArguments();
            categoryArgs.Add(new QueryArgument<StringGraphType> { Name = "code", Description = "Search by unique code." });
            categoryArgs.Add(new QueryArgument<StringGraphType> { Name = "title", Description = "Search by display title." });
            Field(
                name: "categories",
                description: "Categories in the variable.",
                arguments: categoryArgs,
                type: typeof(ListGraphType<CategoryType>),
                resolve: context => {
                    QueryFilterOptions options = new QueryFilterOptions();
                    options.Query.Value = Lucene.BuildQuery(context.Arguments);
                    options.Query.Syntax = Syntax.Lucene;

                    string view = null;
                    if(context.UserContext.ContainsKey($"view-{context.Source.Name}")) view = context.UserContext[$"view-{context.Source.Name}"]?.ToString();

                    return categories.GetAllAsync(context.Source.Name, view, options);
                }
            );

            Field(
                name: "types",
                description: "Category types in the variable.",
                type: typeof(ListGraphType<CategoryTypeType>),
                resolve: context => {
                    QueryFilterOptions options = new QueryFilterOptions();
                    options.Query.Value = Lucene.BuildQuery(context.Arguments);
                    options.Query.Syntax = Syntax.Lucene;

                    string view = null;
                    if(context.UserContext.ContainsKey($"view-{context.Source.Name}")) view = context.UserContext[$"view-{context.Source.Name}"]?.ToString();

                    return categoryTypes.GetAllAsync(context.Source.Name, view, options);
                }
            );

            Field(
                name: "categoryRoot",
                description: "Resolve the root categories for this variable.",
                arguments: new QueryArguments() {
                    new QueryArgument<StringGraphType> { Name = "typeId", Description = "Category type Id to filter categories." },
                    new QueryArgument<StringGraphType> { Name = "hierarchyId", Description = "Hierarchy Id." }
                },
                type: typeof(ListGraphType<CategoryType>),
                resolve: context => {
                    string view = null;
                    if(context.UserContext.ContainsKey($"view-{context.Source.Name}")) view = context.UserContext[$"view-{context.Source.Name}"]?.ToString();

                    return categories.GetRootCategoriesAsync(
                        context.Source.Name,
                        view,
                        context.Arguments.ContainsKey("typeId")? context.Arguments["typeId"].ToString() : null,
                        context.Arguments.ContainsKey("hierarchyId")? context.Arguments["hierarchyId"].ToString() : null,
                        null
                    );
                }
            );

            Field(
                name: "categoryAncestors",
                description: "Resolve the categories that are ancestors of a particular category.",
                arguments: new QueryArguments() {
                    new QueryArgument<NonNullGraphType<StringGraphType>> { Name = "code", Description = "Unique code of the category." },
                    new QueryArgument<StringGraphType> { Name = "typeId", Description = "Category type Id to filter categories." },
                    new QueryArgument<StringGraphType> { Name = "hierarchyId", Description = "Hierarchy Id." }
                },
                type: typeof(ListGraphType<CategoryType>),
                resolve: context => {
                    string view = null;
                    if(context.UserContext.ContainsKey($"view-{context.Source.Name}")) view = context.UserContext[$"view-{context.Source.Name}"]?.ToString();

                    return categories.GetCategoryAncestorsAsync(
                        context.Source.Name,
                        context.Arguments["code"].ToString(),
                        view,
                        context.Arguments.ContainsKey("typeId")? context.Arguments["typeId"].ToString() : null,
                        context.Arguments.ContainsKey("hierarchyId")? context.Arguments["hierarchyId"].ToString() : null,
                        null
                    );
                }
            );

            Field(
                name: "categoryDescendants",
                description: "Resolve the categories that are descendants of a particular category.",
                arguments: new QueryArguments() {
                    new QueryArgument<NonNullGraphType<StringGraphType>> { Name = "code", Description = "Unique code of the category." },
                    new QueryArgument<StringGraphType> { Name = "typeId", Description = "Category type Id to filter categories." },
                    new QueryArgument<StringGraphType> { Name = "hierarchyId", Description = "Hierarchy Id." }
                },
                type: typeof(ListGraphType<CategoryType>),
                resolve: context => {
                    string view = null;
                    if(context.UserContext.ContainsKey($"view-{context.Source.Name}")) view = context.UserContext[$"view-{context.Source.Name}"]?.ToString();

                    return categories.GetCategoryDescendantsAsync(
                        context.Source.Name,
                        context.Arguments["code"].ToString(),
                        view,
                        context.Arguments.ContainsKey("typeId")? context.Arguments["typeId"].ToString() : null,
                        context.Arguments.ContainsKey("hierarchyId")? context.Arguments["hierarchyId"].ToString() : null,
                        null
                    );
                }
            );
        }
    }
}