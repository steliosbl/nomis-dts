using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;

namespace fe_api.GraphQL.Types {
    public class RowMajorObservationsType : ObjectGraphType<RowMajorObservations> {
        public RowMajorObservationsType() {
            Field(
                name: "dimensions",
                description: "Dimensions that identify the record, order here matches codes array.",
                type: typeof(ListGraphType<StringGraphType>),
                resolve: x => x.Source.Dimensions
            );
            Field(
                name: "codes",
                description: "Observation codes",
                type: typeof(ListGraphType<ListGraphType<StringGraphType>>),
                resolve: x => x.Source.Codes
            );
            Field(
                name: "values",
                description: "Observation values in row-major order",
                type: typeof(ListGraphType<DecimalGraphType>),
                resolve: x => x.Source.Values
            );
            Field(
                name: "statuses",
                description: "Observation status codes in row-major order",
                type: typeof(ListGraphType<IntGraphType>),
                resolve: x => x.Source.Statuses
            );
        }
    }
}