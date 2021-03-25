using GraphQL.Types;

using Nomis.Interfaces.Variables.Models;
using Nomis.Interfaces.Variables.Repository;

namespace fe_api.GraphQL.Types {
    public class CategoryType : ObjectGraphType<Category> {
        public CategoryType(ICategoryTypeStore typeStore) {
            Field(x => x.Code).Description("Unique code of category within variable.");
            Field(x => x.Title, nullable: true).Description("Title for display purposes.");
            Field(x => x.TypeId).Description("Type or classification");
            Field(
                name: "ancestors",
                description: "Ancestors of the category",
                type: typeof(ListGraphType<CategoryAncestorType>),
                resolve: x => x.Source.Ancestors
            );
        }
    }
}