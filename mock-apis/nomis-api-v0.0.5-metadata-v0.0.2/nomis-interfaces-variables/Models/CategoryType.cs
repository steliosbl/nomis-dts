using System;

namespace Nomis.Interfaces.Variables.Models {
    public class CategoryType {
        public string Id { get; set; }
        public string Title { get; set; }
        public string TitlePlural { get; set; }
        public string Reference { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();
    }
}