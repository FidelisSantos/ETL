// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use("etl");

db.createCollection("reports", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["_id", "report_id", "type", "created_at", "updated_at", "is_active", "risk", "name", "client", "file", "company", "organization"],
        properties: {
          _id: { bsonType: "objectId" },
          report_id: { bsonType: "string" },
          type: { bsonType: "string" },
          created_at: { bsonType: "date" },
          updated_at: { bsonType: "date" },
          is_active: { bsonType: "bool" },
          risk: { bsonType: "string" },
          name: { bsonType: "string" },
          client: { bsonType: "string" },
          file: { bsonType: "object" },
          company: { bsonType: "object" },
          organization: { bsonType: "object" },
          workstation: { bsonType: "object" }
        }
      }
    }
  });

  db.reports.createIndex({ created_at: 1 });


  db.createCollection("realtime_reports", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["_id", "report_id", "type", "created_at", "updated_at", "is_active", "risk", "name", "client", "file", "company", "organization"],
        properties: {
          _id: { bsonType: "objectId"},
          report_id: { bsonType: "string" },
          type: { bsonType: "string" },
          created_at: { bsonType: "date" },
          updated_at: { bsonType: "date" },
          is_active: { bsonType: "bool" },
          risk: { bsonType: "string" },
          name: { bsonType: "string" },
          client: { bsonType: "string" },
          file: { bsonType: "object" },
          company: { bsonType: "object" },
          organization: { bsonType: "object" },
          workstation: { bsonType: "object" }
        }
      }
    }
  });

  db.realtime_reports.createIndex({ created_at: 1 });

  db.createCollection("report_control", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["_id", "start_date", "end_date", "extracted_at", "rows"],
        properties: {
          _id: { bsonType: "objectId" },
          start_date: { bsonType: "date" },
          end_date: { bsonType: "date" },
          extracted_at: { bsonType: "date" },
          rows: { bsonType: "int" }
        }
      }
    }
  });

  db.report_control.createIndex({ extracted_at: 1 });

  db.createCollection("files", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: [
          "_id",
          "file_id",
          "original_name",
          "generated_name",
          "duration",
          "status",
          "created_at",
          "organization",
          "company",
          "client",
        ],
        properties: {
          _id: { bsonType: "objectId" },
          file_id: { bsonType: "string" },
          original_name: { bsonType: "string" },
          generated_name: { bsonType: "string" },
          duration: { bsonType: "int" },
          status: { bsonType: "string" },
          created_at: { bsonType: "date" },
          client: { bsonType: "string" },
          organization: {
            bsonType: "object",
            required: ["id", "name"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          },
          company: {
            bsonType: "object",
            required: ["id", "name"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          },
          workstation: {
            bsonType: ["object", "null"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          },
          user: {
            bsonType: ["object", "null"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          }
        }
      }
    }
  });
    
  db.file_risks.createIndex({ created_at: 1 });
  
  db.createCollection("realtime_files", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["_id", "organization", "company", "total_files", "has_report", "client"],
        properties: {
          _id: { bsonType: "objectId" },
          client: { bsonType: "string" },
          organization: {
            bsonType: "object",
            required: ["id", "name"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          },
          company: {
            bsonType: "object",
            required: ["id", "name"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          },
          workstation: {
            bsonType: ["object", "null"],
            properties: {
              id: { bsonType: "string" },
              name: { bsonType: "string" }
            }
          },
          total_files: { bsonType: "int" },
          has_report: { bsonType: "int" }
        }
      }
    }
  });
  
  db.createCollection("file_control", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: ["_id", "start_date", "end_date", "extracted_at", "rows"],
        properties: {
          _id: { bsonType: "objectId" },
          start_date: { bsonType: "date" },
          end_date: { bsonType: "date" },
          extracted_at: { bsonType: "date" },
          rows: { bsonType: "int" }
        }
      }
    }
  });

  db.file_control.createIndex({ extracted_at: 1 });
  