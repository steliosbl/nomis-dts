using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;

namespace fe_api.GraphQL.Types {
    public class UnitType : ObjectGraphType<Unit> {
        public UnitType() {
            Field(x => x.Id).Description("Unique unit Id.");
            Field(x => x.Label).Description("Label for display purposes.");
        }
    }
}