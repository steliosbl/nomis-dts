using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;

namespace fe_api.GraphQL.Types {
    public class StatusType : ObjectGraphType<Status> {
        public StatusType() {
            Field(x => x.Id).Description("Unique status Id.");
            Field(x => x.Symbol, nullable: true).Description("Symbol (usually a single character or letter) for display purposes.");
            Field(x => x.Message, nullable: true).Description("Message for display purposes.");
        }
    }
}