using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Metadata.Models;
using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Api.Metadata.Models.Store {
    public class MetadataDbStoreInMemory : IMetadataStore {
        private List<MetaAssociation> _data = null;
        private readonly InMemoryStoreConfiguration _config;
        
        public MetadataDbStoreInMemory(IOptions<InMemoryStoreConfiguration> options) {
            _config = options.Value;
        }

        public async Task<IEnumerable<MetaAssociation>> GetAllAsync(QueryFilterOptions options) {
            SeedData();
            
            await Task.CompletedTask;

            return _data.Where(m => {
                    // Filter should be applied here.
                    return true;
                }
            );
        }

        public async Task<IEnumerable<MetaAssociation>> GetAllBelongingToAsync(Guid id) {
            SeedData();
            
            await Task.CompletedTask;

            // Find associated metadata.
            return _data.Where(m => m.BelongsTo == id);
        }

        public async Task<MetaAssociation> GetAsync(Guid id) {
            SeedData();
            
            await Task.CompletedTask;

            return _data.Where(m => m.Id == id).FirstOrDefault();
        }

        public async Task<MetaAssociation> AddAsync(MetaAssociation meta) {
            SeedData();
            
            // Find out if the entry exists already.
            var m = await GetAsync(meta.Id.Value);

            // New entry.
            if(m == null) {
                _data.Add(meta);
                return meta;
            }
            else return await UpdateAsync(meta); // Update entry.
        }

        public async Task<MetaAssociation> UpdateAsync(MetaAssociation meta) {
            SeedData();
            
            // Get the current entry.
            var entry = await GetAsync(meta.Id.Value);
            if(entry != null) {
                _data.Remove(entry);
                _data.Add(meta);
                return meta;
            }
            else return null; // Entry not found.
        }

        public async Task<bool> DeleteAsync(Guid id) {
            SeedData();

            // Find the existing entry.
            var meta = await GetAsync(id);
            if(meta != null) {
                _data.Remove(meta);
                return true;
            }
            else return true; // Already does not exist.
        }

        private void SeedData() {
            if(_data != null) return; // Don't seed when already initialized.

            // Only seed data if configured to do so.
            if(!_config.SeedData) {
                _data = new List<MetaAssociation>();
                return;
            }

            Guid ownerUUID = Guid.NewGuid(); // This would be the UUID of an object to which metadata is attached.
            Guid ucId = Guid.NewGuid();

            _data = new List<MetaAssociation>() {
                new MetaAssociation() {
                    Id = Guid.NewGuid(),
                    BelongsTo = new Guid("7b9568e3-019e-4faf-8a50-98c66332ba09"),
                    Meta = new List<MetaItem>() {
                        new MetaItem() {
                            Role = "note",
                            Properties = new List<MetaProperty>() {
                                new MetaProperty() { Prefix = "dc", Property = "description", Value = "This is an age variable note" },
                            }
                        }
                    }
                },
                new MetaAssociation() {
                    Id = new Guid("ea35c6ef-2c4c-4a81-9706-4337a5d31d70"),
                    Description = "Statistical disclosure note supplied by ONS (smith@example.com)",
                    Meta = new List<MetaItem>() {
                        new MetaItem() {
                            Role = "note",
                            Properties = new List<MetaProperty>() {
                                new MetaProperty() { Prefix = "dc", Property = "description", Value = "This data is modified to prevent disclosure." }
                            }
                        }
                    }
                },
                new MetaAssociation() {
                    BelongsTo = new Guid("2dc382c4-a0d9-46cf-9ce4-60d045a6498a"),
                    Include = new List<Guid>() { new Guid("ea35c6ef-2c4c-4a81-9706-4337a5d31d70") }
                }
            };
        }
    }
}