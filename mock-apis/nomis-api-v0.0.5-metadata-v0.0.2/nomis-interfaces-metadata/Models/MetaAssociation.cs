using System;
using System.Collections.Generic;

namespace Nomis.Interfaces.Metadata.Models {
    public class MetaAssociation {
        /// <summary>Unique ID for this metadata association.</summary>
        public Guid? Id { get; set; }

        /// <summary>Unique UUID of object to which metadata is primarily attached (optional).</summary>
        public Guid? BelongsTo { get; set; }
        
        /// <summary>Administrative description of the metadata entry.</summary>
        public string Description { get; set; }

        public DateTime? Created { get; set; }

        /// <summary>Date at which the metadata becomes valid.</summary>
        public DateTime? ValidFrom { get; set; }

        /// <summary>Date at which the metadata is no longer valid.</summary>
        public DateTime? ValidTo { get; set; }

        /// <summary>List of related further metadata to include with this association.</summary>
        public ICollection<Guid> Include { get; set; }

        /// <summary>Metadata items</summary>
        public ICollection<MetaItem> Meta { get; set; }

        /// <summary>Indicate if the metadata is valid in regards the valid from and to dates.</summary>
        /// <param name="d">Date point for test of validity.</param>
        /// <returns>True if association is valid based on date.</returns>
        public bool IsValidDate(DateTime d) {
            if( (ValidFrom == null || ValidFrom <= d) &&
                (ValidTo == null || ValidTo >= d)) return true;
            else return false;
        }

        public MetaAssociation() { }

        /// <summary>Create an association by cloning properties from another.</summary>
        public MetaAssociation(MetaAssociation o) {
            this.Id = o.Id;
            this.BelongsTo = o.BelongsTo;
            this.Description = o.Description;
            this.Created = o.Created;
            this.ValidFrom = o.ValidFrom;
            this.ValidTo = o.ValidTo;
            if(o.Include != null) this.Include = new List<Guid>(o.Include);
            if(o.Meta != null) {
                this.Meta = new List<MetaItem>(o.Meta.Count);
                foreach(var m in o.Meta) this.Meta.Add(new MetaItem(m));
            }
        }
    }
}