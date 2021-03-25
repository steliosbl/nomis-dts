using GraphQL.Types;

namespace fe_api.GraphQL.Types {
    public class CategoryTypeType : ObjectGraphType<Nomis.Interfaces.Variables.Models.CategoryType> {
        public CategoryTypeType() {
            Field(x => x.Id).Description("Unique Id of category type within variable.");
            Field(x => x.Title).Description("Title for display purposes.");
            Field(x => x.TitlePlural).Description("Plural version of the title, for display purposes.");
            Field(x => x.Reference).Description("Short reference code, (e.g. `ualad09`).");
        }
    }
}