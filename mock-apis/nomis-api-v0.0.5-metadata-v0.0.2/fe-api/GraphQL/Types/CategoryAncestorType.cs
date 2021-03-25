using GraphQL.Types;

using Nomis.Interfaces.Variables.Models;

namespace fe_api.GraphQL.Types {
    public class CategoryAncestorType : ObjectGraphType<CategoryAncestor> {
        public CategoryAncestorType() {
            Field(x => x.Code).Description("Unique Id of ancestor category.");
            Field(
                name: "hierarchies",
                description: "Hierarchies in which the ancestor relationship applies.",
                type: typeof(ListGraphType<StringGraphType>),
                resolve: context => context.Source.Hierarchies
            );
        }
    }
}