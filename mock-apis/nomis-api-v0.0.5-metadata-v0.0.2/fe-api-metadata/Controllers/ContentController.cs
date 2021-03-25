using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Http;

using Nomis.Interfaces.Metadata.Models;
using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Api.Metadata.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ContentController : ControllerBase
    {
        private readonly ILogger<ContentController> _logger;
        private readonly IMetadataStore _context;
        private MetadataResolver _resolver;

        public ContentController(
            ILogger<ContentController> logger,
            IMetadataStore context)
        {
            _logger = logger;
            _context = context;
            _resolver = new MetadataResolver(_context);
        }


        /// <summary>Get metadata.</summary>
        /// <remarks>
        ///     Get a list of all metadata for an object. This endpoint resolves metadata entries automatically, following
        ///     the `Include` entries and appending these to the `meta`.
        /// </remarks>
        /// <param name="id">UUID of object that requested metadata belongs to.</param>
        /// <returns>List of metadata.</returns>
        [HttpGet("{id}")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        public async Task<IEnumerable<MetaAssociation>> GetAsync(Guid id)
        {
            // Get all matching associations.
            IEnumerable<MetaAssociation> list = await _context.GetAllBelongingToAsync(id);

            // List to place resolved metadata into.
            List<MetaAssociation> resolved = new List<MetaAssociation>();

            foreach(var a in list) {
                // Resolve any "include" links.
                resolved.Add(await _resolver.ResolveAsync(a));
            }

            return resolved;
        }
    }
}
