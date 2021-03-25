using GraphQL.Types;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Core.Helpers;
using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Contacts.Repository;
using Nomis.Interfaces.Datasets.Repository;

namespace fe_api.GraphQL.Types {
    public class DatasetType : ObjectGraphType<Dataset> {
        public DatasetType(
            IDatasetStore datasets,
            IContactStore contacts,
            IDimensionStore dimensions,
            IObservationStore observations,
            IStatusStore status,
            IUnitStore units
        ) {
            Field(x => x.Id).Description("Dataset Id.");
            Field(x => x.Title).Description("Title to label the dataset outputs.");
            Field(x => x.IsAdditive).Description("Data in this dataset are additive.");
            Field(x => x.IsFlagged).Description("Data in this dataset may be flagged.");
            Field(x => x.MinimumRound).Description("Minimum output rounding level allowed.");
            Field(x => x.Online).Description("Online for use.");
            Field(x => x.RestrictedAccess).Description("Data is only available through a specific EUL.");
            Field(x => x.ContactId).Description("Unique Id of the point of contact.");
            Field(
                name: "contact",
                description: "Details for point of contact.",
                type: typeof(ContactType),
                resolve: context => contacts.GetAsync(context.Source.ContactId)
            );
            Field(
                name: "statusCodes",
                description: "Details of assignable observation status codes.",
                type: typeof(ListGraphType<StatusType>),
                resolve: context => status.GetAllAsync(context.Source.Id, null)
            );
            Field(
                name: "units",
                description: "Details of assignable observation units.",
                type: typeof(ListGraphType<UnitType>),
                resolve: context => units.GetAllAsync(context.Source.Id, null)
            );

            QueryArguments dimensionArgs = new QueryArguments();
            dimensionArgs.Add(new QueryArgument<StringGraphType> { Name = "name", Description = "Search by unique name." });
            dimensionArgs.Add(new QueryArgument<StringGraphType> { Name = "label", Description = "Search by display label." });
            dimensionArgs.Add(new QueryArgument<StringGraphType> { Name = "role", Description = "Search by role." });

            Field(
                name: "dimensions",
                description: "Dimensions of this dataset",
                arguments: dimensionArgs,
                type: typeof(ListGraphType<DimensionType>),
                resolve: context => {
                    QueryFilterOptions options = new QueryFilterOptions();
                    options.Query.Value = Lucene.BuildQuery(context.Arguments);
                    options.Query.Syntax = Syntax.Lucene;
                    return dimensions.GetAllAsync(context.Source.Id, options);
                }
            );

            Field(
                name: "values",
                description: "Data stored in this dataset.",
                arguments: new QueryArguments() {
                    new QueryArgument<StringGraphType> { Name = "query", Description = "Filter data by dimension using Lucene syntax (e.g. `geography:E12000001 AND sex:M`) ."}
                },
                type: typeof(RowMajorObservationsType),
                resolve: context => {
                    QueryFilterOptions options = null;

                    // Apply the filter query?
                    if(context.Arguments.ContainsKey("query")) {
                        options = new QueryFilterOptions();
                        options.Query.Value = context.Arguments["query"].ToString();
                        options.Query.Syntax = Syntax.Lucene;
                    }

                    return observations.GetAllAsync(context.Source.Id, options);
                }
            );
        }
    }
}