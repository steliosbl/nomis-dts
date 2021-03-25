using System;
using System.IO;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Contacts.Repository;
using Nomis.Interfaces.Contacts.Models;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class ContactStore : IContactStore {
        private List<Contact> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Contact> AddAsync(Contact contact) {
            await SeedDataAsync();

            seeded.Add(contact);

            return contact;
        }

        public async Task<Contact> UpdateAsync(Contact contact) {
            await SeedDataAsync();

            var c = await GetAsync(contact.Id);

            if(c != null) {
                if(contact.Email != null) c.Email = contact.Email;
                if(contact.Homepage != null) c.Homepage = contact.Homepage;
                if(contact.Name != null) c.Name = contact.Name;
                if(contact.Phone != null) c.Phone = contact.Phone;
            }
            
            return c;
        }

        public async Task<bool> DeleteAsync(string id) {
            await SeedDataAsync();

            var contact = await GetAsync(id);
            if(contact != null) return seeded.Remove(contact);
            else return true; // Didn't exist anyway.
        }
        
        public async Task<Contact> GetAsync(string id) {
            await SeedDataAsync();

            return seeded.Find(c => c.Id == id);
        }
        public async Task<List<Contact>> GetAllAsync(QueryFilterOptions options = null) {
            await SeedDataAsync();

            return seeded;
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return;
            else seeded = new List<Contact>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add(new Contact() {
                    Id = "ons",
                    Name = "National Statistics Enquiry Point",
                    Phone = "+44 (0)845 6013034",
                    Email = "info@statisitcs.gov.uk",
                    Homepage = "https://www.ons.gov.uk"
                }
            );

            seeded.Add(new Contact() {
                    Id = "census",
                    Name = "Census Customer Services",
                    Phone = "+44 (0)1329 444972",
                    Email = "census.customerservices@ons.gov.uk",
                    Homepage = "https://www.ons.gov.uk/census"
                }
            );

            seeded.Add(new Contact() {
                    Id = "nomis",
                    Name = "Nomis Helpdesk",
                    Phone = null,
                    Email = "support@nomisweb.co.uk",
                    Homepage = "https://www.nomisweb.co.uk"
                }
            );

            await Task.CompletedTask;
        }

        public ContactStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;
        }
    }
}