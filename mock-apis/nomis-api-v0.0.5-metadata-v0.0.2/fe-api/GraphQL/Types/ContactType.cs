using System.Collections.Generic;
using GraphQL.Types;

using Nomis.Interfaces.Contacts.Models;
using Nomis.Interfaces.Contacts.Repository;

namespace fe_api.GraphQL.Types {
    public class ContactType : ObjectGraphType<Contact> {
        public ContactType(IContactStore contacts) {
            Field(x => x.Id).Description("Contact Id.");
            Field(x => x.Name, nullable: true).Description("Name of person or organisation.");
            Field(x => x.Email, nullable: true).Description("Email address.");
            Field(x => x.Homepage, nullable: true).Description("Web page.");
            Field(x => x.Phone, nullable: true).Description("Phone number.");
        }
    }
}