using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Variables.Repository;

namespace fe_api.GraphQL.Types {
    public class DimensionType : ObjectGraphType<Dimension> {
        public DimensionType(IDimensionStore dimensions, IVariableStore variables) {
            Field(x => x.Name).Description("Unique name of dimension.");
            Field(x => x.Label).Description("Label for display purposes.");
            Field(x => x.IsAdditive).Description("This dimension can have user-defined categories.");
            Field<VariableMappingType>(
                name: "variableMapping",
                description: "Variable mapped to from the dimension.",
                resolve: x => x.Source.Variable);
            Field<VariableType>(
                name: "variable",
                description: "Variable mapped to this dimension.",
                resolve: x=> {
                    if(x.Source.Variable == null) return null;
                    else {
                        // Pass view into user context for downstream resolvers.
                        x.UserContext[$"view-{x.Source.Variable.Name}"] = x.Source.Variable.View;

                        return variables.GetAsync(x.Source.Variable.Name, x.Source.Variable.View);
                    }
                }
            );
            Field<DimensionRoleType>(
                name: "role",
                description: "Role played by the dimension.",
                resolve: x => x.Source.Role);
            Field(x => x.CanFilter).Description("This dimension can be used to filter observations.");
            Field(
                name: "defaults",
                description: "Default selections of categories.",
                resolve: x => x.Source.Defaults,
                type: typeof(ListGraphType<StringGraphType>)
            );
        }
    }
}