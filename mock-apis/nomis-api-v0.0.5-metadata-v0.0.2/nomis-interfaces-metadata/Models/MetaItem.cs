using System;
using System.Collections.Generic;

namespace Nomis.Interfaces.Metadata.Models {
    public class MetaItem {
        public Guid? OriginId { get; private set; }
        public string Role { get; set; }
        public ICollection<MetaProperty> Properties { get; set; }

        public void SetOriginId(Guid? origin) {
            OriginId = origin;
        }

        public MetaItem() { }

        public MetaItem(MetaItem o) {
            this.OriginId = o.OriginId;
            this.Role = o.Role;
            if(o.Properties != null) {
                this.Properties = new List<MetaProperty>(o.Properties.Count);
                foreach(var p in o.Properties) this.Properties.Add(new MetaProperty(p));
            }
        }
    }
}