import labelbox as lb


client = lb.Client(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbHhkcHhpa3owYW40MDcwb2V1dGVkbGNzIiwib3JnYW5pemF0aW9uSWQiOiJjbHhkcHhpa2wwYW4zMDcwbzE5d2RnOXpnIiwiYXBpS2V5SWQiOiJjbHhkdmt2NXgwMG5vMDcyMmcxYnBjc2U3Iiwic2VjcmV0IjoiNzg5MDBmYzUxYjYxMmNhYWVmMzg2Y2I3OTE5ODVkZTIiLCJpYXQiOjE3MTgzMjAzNjQsImV4cCI6MjM0OTQ3MjM2NH0.kt5MOWVDv0ArrHfKXHT7Jr3nANO4sHKyRjDelXovOTc")


dataset = client.get_dataset("clxdpz68c00040738t0k03vk6")


# Create data payload
# Use global key, a unique ID to identify an asset throughout Labelbox workflow. Learn more: https://docs.labelbox.com/docs/global-keys
# You can add metadata fields to your data rows. Learn more: https://docs.labelbox.com/docs/import-metadata
assets = [
 {
   "row_data": "https://lb-test-data.s3.us-west-1.amazonaws.com/video-samples/sample-video-1.mp4",
   "global_key": "example-video-0001",
   "media_type": "VIDEO",
   "metadata_fields": [{"schema_id": "cko8s9r5v0001h2dk9elqdidh", "value": "my tag"}],
   "attachments":  [{"type": "IMAGE_OVERLAY", "value": "https://storage.googleapis.com/labelbox-sample-datasets/Docs/rgb.jpg"},
                   {"type": "IMAGE_OVERLAY", "value": "https://storage.googleapis.com/labelbox-sample-datasets/Docs/cir.jpg"},
                   {"type": "IMAGE_OVERLAY", "value": "https://storage.googleapis.com/labelbox-sample-datasets/Docs/weeds.jpg"},
                   {"type": "RAW_TEXT", "value": "IOWA, Zone 2232, June 2022 [Text string]"},
                   {"type": "TEXT_URL", "value": "https://storage.googleapis.com/labelbox-sample-datasets/Docs/text_attachment.txt"},
                   {"type": "IMAGE", "value": "https://storage.googleapis.com/labelbox-sample-datasets/Docs/disease_attachment.jpeg"},
                   {"type": "VIDEO", "value":  "https://storage.googleapis.com/labelbox-sample-datasets/Docs/drone_video.mp4"},
                   {"type": "HTML", "value": "https://storage.googleapis.com/labelbox-sample-datasets/Docs/windy.html"}],
 }
]
# Bulk add data rows to the dataset
task = dataset.create_data_rows(assets)


task.wait_till_done()
print(task.errors)