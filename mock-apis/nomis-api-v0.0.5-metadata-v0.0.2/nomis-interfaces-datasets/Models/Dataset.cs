using System;
namespace Nomis.Interfaces.Datasets.Models {
    public class Dataset {
        public string Id { get; set; }
        public string Title { get; set; }
        public string ContactId { get; set; }
        public bool IsAdditive { get; set; } = true;
        public bool IsFlagged { get; set; } = true;
        public string DerivedFrom { get; set; }
        public bool RestrictedAccess { get; set; } = false;
        public int MinimumRound { get; set; } = 0;
        public bool Online { get; set; } = false;
        public Guid UUID { get; set; } = Guid.NewGuid();

        public Dataset() { }
    }
}