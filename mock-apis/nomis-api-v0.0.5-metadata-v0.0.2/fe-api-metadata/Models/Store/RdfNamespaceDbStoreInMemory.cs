using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Metadata.Models;
using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Api.Metadata.Models.Store {
    public class RdfNamespaceDbStoreInMemory : IRdfNamespaceStore {
        private List<RdfNamespace> _data;
        private readonly InMemoryStoreConfiguration _config;

        public RdfNamespaceDbStoreInMemory(IOptions<InMemoryStoreConfiguration> options) {
            _config = options.Value;
        }

        public async Task<IEnumerable<RdfNamespace>> GetAllAsync() {
            SeedData();
            
            await Task.CompletedTask;
            return _data;
        }

        public async Task<RdfNamespace> GetAsync(string prefix) {
            SeedData();
            
            await Task.CompletedTask;
            
            return _data.Where(c => c.Prefix == prefix).SingleOrDefault();
        }

        public async Task<bool> AddAsync(RdfNamespace rdf) {
            SeedData();
            
            // Find out if the entry exists already.
            var m = await GetAsync(rdf.Prefix);

            // New entry.
            if(m == null) {
                _data.Add(rdf);
                return true;
            }
            else return await UpdateAsync(rdf); // Update entry.
        }

        public async Task<bool> UpdateAsync(RdfNamespace rdf) {
            SeedData();
            
            // Get the current entry.
            var entry = await GetAsync(rdf.Prefix);
            if(entry != null) {
                // Make changes.
                entry.Description = rdf.Description;
                entry.Url = rdf.Url;
                
                return true;
            }
            else return false; // Entry not found.

        }

        public async Task<bool> DeleteAsync(string id) {
            SeedData();
            
            // Find the existing entry.
            var entry = await GetAsync(id);
            if(entry != null) {
                // Remove the entry.
                return _data.Remove(entry);
            }
            else return true; // Already does not exist.
        }

        private void SeedData() {
            if(_data != null) return; // Don't seed when already initialized.
            else _data = new List<RdfNamespace>();

            if(_config.SeedData) {
                _data.Add(new RdfNamespace() {
                    Prefix = "dc",
                    Description = "Dublin Core",
                    Url = "http://dublincore.org/specifications/dublin-core/dcmi-terms/2020-01-20/"
                });
            }
        }
    }
}