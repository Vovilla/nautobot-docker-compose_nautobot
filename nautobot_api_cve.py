import uuid

myuuid = uuid.uuid4()

print(str(myuuid))


Junos 17.1R1.1


  "alias": "string",
  "release_date": "2022-11-25",
  "end_of_support": "2022-11-25",
  "documentation_url": "string",
  "software_images": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "long_term_support": true,
  "pre_release": true,
  "custom_fields": {},
  "tags": [
    {
      "name": "string",
      "slug": "string",
      "color": "string"
    }
  ]
  
  
# post software. Для создания software можно не использовать software_image!!!
{
  "device_platform": "2f1206eb-7c5c-4203-9240-85dfdbe390a8",
  "version": "17.1R1.1"
}


# post cve
{
  "name": "CVE111",
  "published_date": "2022-11-25",
  "link": "http://link.com",
  "severity": "Critical",
  "relationships": {
    "soft_cve": {
      "source": {
        "objects": [
          {
            "id": "9d94ebeb-4411-4e48-882f-1715c94b378b"
          }
        ]
      }
    }
  }
}

# put cve to software