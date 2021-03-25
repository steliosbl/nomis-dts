# Metadata API

## Introduction
The Metadata API provides a mechanism for storing groups of metadata.

Multiple groups of metadata properties can be defined against a single metadata Id (UUID).
Each group having its a role, which for example could be a `note` or `warning`
etc.

The metadata is not hierarchical in nature.

## Endpoints

- `/content` the intended endpoint where metadata should be accessed.
- `/rdf-namespaces` defines the valid namespaces for metadata properties.
- `/roles` defines the roles that metadata groups can serve.
- `/definitions` the actual metadata definitions.
- `/swagger` OAS 3.0 documentation for the service.

## Concepts for attaching metadata
There are two ways of associate metadata to an object, directly and indirectly.

### Direct association
Direct association is used for very specific metadata about an object, that typically
isn't intended to be re-used by other objects.

A direct association is made by specifying the object's UUID in the `belongsTo` field
of the metadata association.

### Indirect association
Indirect association is useful for re-using metadata. Typically (although not always)
metadata which is indirectly attached, has no directly attached object (i.e. `belongsTo == null`).

Indirect association is made by adding one or more metadata Ids to the `include`
array property of an existing metadata association, typically one where an object's UUID
is set in the `belongsTo` field.

## Examples
The following example explores creating and associating metadata:

**UUIDs**
- `2dc382c4-a0d9-46cf-9ce4-60d045a6498a`: the UUID of a new Census dataset.
- `ea35c6ef-2c4c-4a81-9706-4337a5d31d70`: Id of some metadata containing a statistical disclosure warning.
- `7b9568e3-019e-4faf-8a50-98c66332ba09`: the UUID of an "Age" variable.

We can create some metadata for "Age" using:

```
POST /definitions

  {
    "belongsTo": "7b9568e3-019e-4faf-8a50-98c66332ba09",
    "meta": [
      {
        "role": "note",
        "properties": [
          {
            "prefix": "dc",
            "property": "description",
            "value": "This is an age variable note"
          }
        ]
      }
    ]
  }
```

The consumer of the metadata would request `/content/7b9568e3-019e-4faf-8a50-98c66332ba09`
and this would return the "Age" metadata.

We can create some re-usable metadata for a statistical disclosure note:

```
POST /definitions

  {
    "description": "Statistical disclosure note supplied by ONS (smith@example.com)",
    "meta": [
      {
        "role": "note",
        "properties": [
          {
            "prefix": "dc",
            "property": "description",
            "value": "This data is modified to prevent disclosure."
          }
        ]
      }
    ]
  }
```

Then assuming the `POST` request created metadata with an Id of `ea35c6ef-2c4c-4a81-9706-4337a5d31d70`,
attach that metadata to the new Census dataset (and potentally others if re-using):

```
POST /definitions

  {
    "belongsTo": "2dc382c4-a0d9-46cf-9ce4-60d045a6498a",
    "include": [ "ea35c6ef-2c4c-4a81-9706-4337a5d31d70" ]
  }
```

The consumer of the metadata would request `/content/2dc382c4-a0d9-46cf-9ce4-60d045a6498a`
and this would return a fully resolved set of metadata (the disclosure note), marked with
`OriginId` properties to show where the groups of metadata each originated.

## Compiling

- Build using `dotnet build`

## Dependencies

- https://github.com/nomisweb/nomis-interfaces-core
- https://github.com/nomisweb/nomis-interfaces-metadata
- Swashbuckle (for Swagger endpoint)

### Stores
There are some in-memory stores to serve for development purposes,
but it is intended that these will be replaced with versions from
`nomis-legacy-metadata` when used with a Nomis backend system.