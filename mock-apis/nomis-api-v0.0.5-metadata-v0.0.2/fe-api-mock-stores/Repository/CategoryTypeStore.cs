using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Variables.Models;
using Nomis.Interfaces.Variables.Repository;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class CategoryTypeStore : ICategoryTypeStore {
        private Dictionary<string, List<CategoryType>> seeded;
        private readonly StoreConfiguration _config;

        public async Task<CategoryType> AddAsync(string variableName, CategoryType type) {
            await SeedDataAsync();

            if(!seeded.ContainsKey(variableName)) seeded.Add(variableName, new List<CategoryType>() { type });
            else seeded[variableName].Add(type);

            return type;
        }

        public async Task<CategoryType> UpdateAsync(string variableName, CategoryType type) {
            await SeedDataAsync();

            CategoryType t = await GetAsync(variableName, type.Id, null);

            if(t != null) {
                if(type.Title != null) t.Title = type.Title;
                if(type.TitlePlural != null) t.TitlePlural = type.TitlePlural;
            }

            return t;
        }

        public async Task<bool> DeleteAsync(string variableName, string typeId) {
            await SeedDataAsync();

            CategoryType type = await GetAsync(variableName, typeId, null);
            
            if(type != null) return seeded[variableName].Remove(type);
            else return true; // Din't exist anyway.
        }

        public async Task<bool> DeleteAllAsync(string variableName) {
            await SeedDataAsync();

            if(seeded.ContainsKey(variableName)) {
                seeded[variableName].Clear();
                return true;
            }
            else return true; // Didn't exist anyway.
        }
        
        public async Task<CategoryType> GetAsync(string variableName, string typeId, string view) {
            await SeedDataAsync();

            List<CategoryType> types = await GetAllAsync(variableName, null, null);

            if(types != null) return types.Find(t => t.Id == typeId);
            else return null;
        }

        public async Task<List<CategoryType>> GetAllAsync(string variableName, string view, QueryFilterOptions options) {
            await SeedDataAsync();

            if(seeded.ContainsKey(variableName)) return seeded[variableName];
            else return null;
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return;
            else seeded = new Dictionary<string, List<CategoryType>>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add(
                "GEOGRAPHY",
                new List<CategoryType>() {
                    new CategoryType() {
                        Id = "480",
                        Title = "Region",
                        TitlePlural = "Regions"
                    }
                }
            );

            seeded.Add(
                "MARSTAT_6",
                new List<CategoryType>() {
                    new CategoryType() {
                        Id = "0",
                        Title = "Not classified",
                        TitlePlural = "Not classified"
                    }
                }
            );

            seeded.Add(
                "AGE_7",
                new List<CategoryType>() {
                    new CategoryType() {
                        Id = "0",
                        Title = "Not classified",
                        TitlePlural = "Not classified"
                    }
                }
            );

            seeded.Add(
                "LIV_ARR",
                new List<CategoryType>() {
                    new CategoryType() {
                        Id = "0",
                        Title = "Living in a couple",
                        TitlePlural = "Living as couples"
                    },
                    new CategoryType() {
                        Id = "1",
                        Title = "Not living in a couple",
                        TitlePlural = "Not living as couples"
                    }
                }
            );

            seeded.Add(
                "SEX",
                new List<CategoryType>() {
                    new CategoryType() {
                        Id = "0",
                        Title = "Not classified",
                        TitlePlural = "Not classified"
                    }
                }
            );
            
            
            
            await Task.CompletedTask;
        }

        public CategoryTypeStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;

        }
    }
}