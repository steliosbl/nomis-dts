using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Variables.Models;
using Nomis.Interfaces.Variables.Repository;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class CategoryStore : ICategoryStore {
        private Dictionary<string, List<Category>> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Category> AddAsync(string variableName, Category category) {
            await SeedDataAsync();

            if(!seeded.ContainsKey(variableName)) seeded.Add(variableName, new List<Category>() { category });
            else seeded[variableName].Add(category);
            
            return category;
        }

        public async Task<Category> UpdateAsync(string variableName, Category category) {
            await SeedDataAsync();

            Category c = await GetAsync(variableName, category.Code, null);

            if(c != null) {
                if(category.Keyval != int.MinValue) c.Keyval = category.Keyval;
                if(category.Title != null) c.Title = category.Title;
                if(category.TypeId != null) c.TypeId = category.TypeId;
            }

            return c;
        }

        public async Task<bool> DeleteAsync(string variableName, string code) {
            await SeedDataAsync();

            List<Category> cats = await GetAllAsync(variableName, null, null);
            Category c = await GetAsync(variableName, code, null);

            if(cats != null && c != null) return cats.Remove(c);
            else return true; // Didn't exist anyway.
        }

        public async Task<bool> DeleteAllAsync(string variableName) {
            await SeedDataAsync();

            List<Category> cats = await GetAllAsync(variableName, null, null);
            if(cats != null) {
                cats.Clear();
            }

            return true;
        }
        
        public async Task<Category> GetAsync(string variableName, string code, string view) {
            await SeedDataAsync();

            List<Category> cats = await GetAllAsync(variableName, view, null);
            return cats.Find(c => c.Code == code);
        }

        public async Task<List<Category>> GetAllAsync(string variableName, string view, QueryFilterOptions options) {
            await SeedDataAsync();

            if(seeded.ContainsKey(variableName)) return seeded[variableName];
            else return null;
        }

        public async Task<List<Category>> GetRootCategoriesAsync(
            string variableName,
            string view,
            string typeId,
            string hierarchyId,
            QueryFilterOptions options) {
                await SeedDataAsync();

                var list = new List<Category>();
                var categories = await GetAllAsync(variableName, view, null);

                list.Add(categories[0]);
                
                return list;
            }


        public async Task<List<Category>> GetCategoryAncestorsAsync(
            string variableName,
            string code,
            string view,
            string typeId,
            string hierarchyId,
            QueryFilterOptions options) {
                return await GetAllAsync(variableName, view, options);
            }

        public async Task<List<Category>> GetCategoryDescendantsAsync(
            string variableName,
            string code,
            string view,
            string typeId,
            string hierarchyId,
            QueryFilterOptions options) {
                return await GetAllAsync(variableName, view, options);
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return;
            else seeded = new Dictionary<string, List<Category>>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add(
                "GEOGRAPHY",
                new List<Category>() {
                    new Category() { Code = "E12000001", Title = "North East", TypeId = "480" },
                    new Category() { Code = "E12000002", Title = "North West", TypeId = "480" },
                    new Category() { Code = "E12000003", Title = "Yorkshire and The Humber", TypeId = "480" },
                    new Category() { Code = "E12000004", Title = "East Midlands", TypeId = "480" },
                    new Category() { Code = "E12000005", Title = "West Midlands", TypeId = "480" },
                    new Category() { Code = "E12000006", Title = "East", TypeId = "480" },
                    new Category() { Code = "E12000007", Title = "London", TypeId = "480" },
                    new Category() { Code = "E12000008", Title = "South East", TypeId = "480" },
                    new Category() { Code = "E12000009", Title = "South West", TypeId = "480" },
                    new Category() { Code = "W92000004", Title = "North East", TypeId = "480" }
                }
            );

            seeded.Add(
                "MARSTAT_6",
                new List<Category>() {
                    new Category() { Code = "1", Title = "Single (never married or never registered a same-sex civil partnership)", TypeId = "0" },
                    new Category() { Code = "2", Title = "Married", TypeId = "0" },
                    new Category() { Code = "3", Title = "In a registered same-sex civil partnership", TypeId = "0" },
                    new Category() { Code = "4", Title = "Separated (but still legally married or still legally in a same-sex civil partnership)", TypeId = "0" },
                    new Category() { Code = "5", Title = "Divorced or formerly in a same-sex civil partnership which is now legally dissolved", TypeId = "0" },
                    new Category() { Code = "6", Title = "Widowed or surviving partner from a same-sex civil partnership", TypeId = "0" }
                }
            );

            seeded.Add(
                "AGE_7",
                new List<Category>() {
                    new Category() { Code = "1", Title = "Age 24 and under", TypeId = "0" },
                    new Category() { Code = "2", Title = "Age 25 to 34", TypeId = "0" },
                    new Category() { Code = "3", Title = "Age 35 to 49", TypeId = "0" },
                    new Category() { Code = "4", Title = "Age 50 to 64", TypeId = "0" },
                    new Category() { Code = "5", Title = "Age 65 to 74", TypeId = "0" },
                    new Category() { Code = "6", Title = "Age 75 to 84", TypeId = "0" },
                    new Category() { Code = "7", Title = "Age 85 and over", TypeId = "0" }
                }
            );

            seeded.Add(
                "SEX",
                new List<Category>() {
                    new Category() { Code = "1", Title = "Male", TypeId = "0" },
                    new Category() { Code = "2", Title = "Female", TypeId = "0" }
                }
            );

            seeded.Add(
                "LIV_ARR",
                new List<Category>() {
                    new Category() { Code = "1", Title = "Living in a couple: Married or in a registered same-sex civil partnership", TypeId = "0" },
                    new Category() { Code = "2", Title = "Living in a couple: Cohabiting", TypeId = "0" },
                    new Category() { Code = "3", Title = "Not living in a couple: Single (never married or never registered a same-sex civil partnership)", TypeId = "1" },
                    new Category() { Code = "4", Title = "Not living in a couple: Married or in a registered same-sex civil partnership", TypeId = "1" },
                    new Category() { Code = "5", Title = "Not living in a couple: Separated (but still legally married or still legally in a same-sex civil partnership)", TypeId = "1" },
                    new Category() { Code = "6", Title = "Not living in a couple: Divorced or formerly in a same-sex civil partnership which is now legally dissolved", TypeId = "1" },
                    new Category() { Code = "7", Title = "Not living in a couple: Widowed or surviving partner from a same-sex civil partnership", TypeId = "1" }
                }
            );

            await Task.CompletedTask;
        }

        public CategoryStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;

        }
    }
}