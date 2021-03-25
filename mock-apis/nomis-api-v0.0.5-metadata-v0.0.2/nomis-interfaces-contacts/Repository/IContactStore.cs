using System.IO;
using System.Threading.Tasks;
using System.Collections.Generic;

using Nomis.Interfaces.Contacts.Models;
using Nomis.Interfaces.Core.Models;

namespace Nomis.Interfaces.Contacts.Repository {
    public interface IContactStore {
        Task<Contact> AddAsync(Contact contact);
        Task<Contact> UpdateAsync(Contact contact);
        Task<bool> DeleteAsync(string id);
        
        Task<Contact> GetAsync(string id);
        Task<List<Contact>> GetAllAsync(QueryFilterOptions options);
    }
}