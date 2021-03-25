using System;

namespace Nomis.Interfaces.Contacts.Models {
    public class Contact {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Homepage { get; set; }
        public string Phone { get; set; }
        public string Email { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();

        public Contact() { }
    }
}