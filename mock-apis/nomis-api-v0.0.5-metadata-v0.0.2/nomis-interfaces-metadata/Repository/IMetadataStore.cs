using System;
using System.Threading.Tasks;
using System.Collections.Generic;

using Nomis.Interfaces.Core.Models;
using Nomis.Interfaces.Metadata.Models;

namespace Nomis.Interfaces.Metadata.Repository {
    public interface IMetadataStore {
        Task<MetaAssociation> AddAsync(MetaAssociation meta);
        Task<MetaAssociation> UpdateAsync(MetaAssociation meta);
        Task<bool> DeleteAsync(Guid id);

        Task<IEnumerable<MetaAssociation>> GetAllAsync(QueryFilterOptions options);
        Task<IEnumerable<MetaAssociation>> GetAllBelongingToAsync(Guid id);
        Task<MetaAssociation> GetAsync(Guid id);
    }
}