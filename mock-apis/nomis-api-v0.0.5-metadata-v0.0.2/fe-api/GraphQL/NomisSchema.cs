using System;

using Microsoft.Extensions.DependencyInjection;

using GraphQL.Types;

using fe_api.GraphQL;

namespace fe_api.GraphQL {
    public class NomisSchema : Schema {
        public NomisSchema(IServiceProvider serviceProvider) : base(serviceProvider) {
            Query = serviceProvider.GetRequiredService<NomisQuery>();
        }
    }
}