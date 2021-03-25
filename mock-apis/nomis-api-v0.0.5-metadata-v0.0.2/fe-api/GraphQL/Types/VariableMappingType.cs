using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;

namespace fe_api.GraphQL.Types {
    public class VariableMappingType : ObjectGraphType<VariableMapping> {
        public VariableMappingType() {
            Field(x => x.Name).Description("Name of the variable mapped to a dimension.");
            Field(x => x.View, nullable: true).Description("View to apply to variable to restrict available categories.");
        }
    }
}