using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Metadata.Repository;

namespace Nomis.Interfaces.Metadata.Models {
    public class MetadataResolver {
        private readonly IMetadataStore _context;

        public MetadataResolver(IMetadataStore context) {
            _context = context;
        }

        /// <summary>Resolve the "include" array property recursively.</summary>
        /// <returns>A resolved clone of the target, or `null` if the target is not within date validity.</returns>
        public async Task<MetaAssociation> ResolveAsync(MetaAssociation target) {
            // When date validity is not met, return a null object reference.
            if(!target.IsValidDate(DateTime.Now)) return null;

            // Clone the target.
            target = new MetaAssociation(target);

            // Make a note of the origin of the metadata.
            if(target.Meta != null) {
                foreach(var m in target.Meta) { if(m.OriginId == null) m.SetOriginId(target.Id.Value); }
            }

            // Does the association have any "include" entries?
            if(target.Include != null) {
                // Follow each include in turn.
                foreach(var id in target.Include) {
                    // Get the entry from storage.
                    var entry = await _context.GetAsync(id);

                    // An entry matching the id was found.
                    if(entry != null) {
                        // Resolve it.
                        var ent = await ResolveAsync(entry);

                        // Did we get a resolved entry back?
                        if(ent != null) {
                            foreach(var m in ent.Meta) {
                                // Make a note of the origin of the metadata.
                                if(m.OriginId == null) m.SetOriginId(id);
                                
                                if(target.Meta == null) target.Meta = new List<MetaItem>();
                                target.Meta.Add(m);
                            }
                        }
                    }
                }
            }

            return target;
        }
    }
}