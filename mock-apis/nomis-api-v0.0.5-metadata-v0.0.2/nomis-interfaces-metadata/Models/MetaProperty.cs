namespace Nomis.Interfaces.Metadata.Models {
    public class MetaProperty {
        public string Prefix { get; set; }

        public string Property { get; set; }

        public string Value { get; set; }

        public MetaProperty() { }

        public MetaProperty(MetaProperty o) {
            this.Prefix = o.Prefix;
            this.Property = o.Property;
            this.Value = o.Value;
        }
    }
}