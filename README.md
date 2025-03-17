# DevHub CMS MCP

A Model Context Protocol (MCP) integration for managing content in the DevHub CMS system.

## Installation

The easiest way to install this package is using the [uv](https://github.com/astral-sh/uv) package manager:

```bash
uv install devhub-cms-mcp
```

You can also install it using pip:

```bash
pip install devhub-cms-mcp
```

## Configuration

This MCP requires the following environment variables to be set:

```bash
export DEVHUB_API_KEY="your_api_key"
export DEVHUB_API_SECRET="your_api_secret"
export DEVHUB_BASE_URL="https://yourbrand.cloudfrontend.net"
```

## Available Tools

This MCP provides the following tools for interacting with DevHub CMS:

### Location Management

- **get_hours_of_operation(location_id)**: Gets the hours of operation for a specific DevHub location. Returns a structured list of time ranges for each day of the week.
- **update_hours(location_id, new_hours, hours_type='primary')**: Updates the hours of operation for a DevHub location.
- **get_nearest_location(business_id, latitude, longitude)**: Finds the nearest DevHub location based on geographic coordinates.

### Content Management

- **get_blog_post(post_id)**: Retrieves a single blog post by ID, including its title, date, and HTML content.
- **create_blog_post(site_id, title, content)**: Creates a new blog post. The content should be in HTML format and should not include an H1 tag.
- **update_blog_post(post_id, title=None, content=None)**: Updates an existing blog post's title and/or content.

### Media Management

- **upload_image(base64_image_content, filename)**: Uploads an image to the DevHub media gallery. Supports webp, jpeg, and png formats. The image must be provided as a base64-encoded string.

## Usage with LLMs

This MCP is designed to be used with Large Language Models that support the Model Context Protocol. It allows LLMs to manage content in DevHub CMS without needing direct API access.