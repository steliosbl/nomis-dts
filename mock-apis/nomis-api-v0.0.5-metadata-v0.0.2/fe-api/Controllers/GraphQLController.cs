using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;

using GraphQL;
using GraphQL.Types;
using GraphQL.SystemTextJson;

namespace fe_api.Controllers
{
    public class GraphQLQuery
    {
        public string OperationName { get; set; }
        public string NamedQuery { get; set; }
        public string Query { get; set; }
        public string Variables { get; set; }
    }

    [ApiExplorerSettings(IgnoreApi = true)]
    [Route("graphql")]
    public class GraphQLController : Controller
    {
        private readonly ISchema _schema;
        private readonly IDocumentExecuter _executer;
        public GraphQLController(ISchema schema, 
        IDocumentExecuter executer)
        {
            _schema = schema;
            _executer = executer;
        }

        [HttpPost]
        public async Task<IActionResult> Post([FromBody]GraphQLQuery query)
        {
            var result = await _executer.ExecuteAsync(_ =>
            {
                _.Schema = _schema;
                _.Query = query.Query;
                _.Inputs = query.Variables?.ToInputs();
                
            });
            if(result.Errors?.Count > 0)
            {
                return BadRequest(result.Errors);
            }
            return Ok(result.Data);
        }
    }
}