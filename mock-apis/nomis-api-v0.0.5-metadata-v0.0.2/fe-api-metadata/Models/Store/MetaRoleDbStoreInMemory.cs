using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Metadata.Models;
using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Api.Metadata.Models.Store {
    public class MetaRoleDbStoreInMemory : IMetaRoleStore {
        private List<MetaItemRole> _data;
        private readonly InMemoryStoreConfiguration _config;

        public MetaRoleDbStoreInMemory(IOptions<InMemoryStoreConfiguration> options) {
            _config = options.Value;
        }

        public async Task<IEnumerable<MetaItemRole>> GetAllAsync() {
            SeedData();
            
            await Task.CompletedTask;
            return _data;
        }
        public async Task<MetaItemRole> GetAsync(string role) {
            await Task.CompletedTask;
            return _data.Where(c => c.Role == role).SingleOrDefault();
        }

        public async Task<bool> AddAsync(MetaItemRole role) {
            SeedData();
            
            // Find out if the entry exists already.
            var m = await GetAsync(role.Role);

            // New entry.
            if(m == null) {
                _data.Add(role);
                return true;
            }
            else return await UpdateAsync(role); // Update entry.
        }

        public async Task<bool> UpdateAsync(MetaItemRole role) {
            SeedData();
            
            // Get the current entry.
            var entry = await GetAsync(role.Role);
            if(entry != null) {
                // Make changes.
                entry.Description = role.Description;

                return true;
            }
            else return false; // Entry not found.
        }

        public async Task<bool> DeleteAsync(string role) {
            SeedData();

            // Find the existing entry.
            var entry = await GetAsync(role);

            if(entry != null) {
                // Remove the entry.
                _data.Remove(entry);

                return true;
            }
            else return true; // Already does not exist.
        }

        private void SeedData() {
            if(_data != null) return; // Don't seed when already initialized.
            else _data = new List<MetaItemRole>();

            if(_config.SeedData) {
                // Set up some demo roles.
                _data.Add(new MetaItemRole() { Role = "note", Description = "Informational note" });
                _data.Add(new MetaItemRole() { Role = "warning", Description = "Warning message" });
                _data.Add(new MetaItemRole() { Role = "sys", Description = "Technical systems properties" });
            }
        }
    }
}