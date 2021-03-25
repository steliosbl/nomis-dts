using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Variables.Repository;

namespace fe_api.GraphQL.Types {
    public class DimensionMappingType : ObjectGraphType<DimensionMapping> {
        public DimensionMappingType(ICategoryStore categories) {
            Field(x => x.Name).Description("Name of the dimension.");
            Field(x => x.Code).Description("Category code.");
        }
    }
}