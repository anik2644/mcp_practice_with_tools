# find_mcp_servers.py
import subprocess
import json
import requests


def search_npm_for_mcp():
    """Search npm for available MCP servers"""
    print("🔍 Searching for MCP servers on npm...")

    # Try to search npm
    try:
        result = subprocess.run(
            ["npm", "search", "@modelcontextprotocol", "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            packages = json.loads(result.stdout)
            print(f"✅ Found {len(packages)} MCP packages:")

            mcp_servers = []
            for pkg in packages:
                name = pkg.get('name', '')
                if 'server' in name.lower():
                    version = pkg.get('version', 'unknown')
                    desc = pkg.get('description', '')[:100]
                    print(f"   • {name} (v{version})")
                    print(f"     {desc}")
                    print()
                    mcp_servers.append(name)

            return mcp_servers
        else:
            print("❌ npm search failed")

    except Exception as e:
        print(f"❌ Error: {e}")

    return []


def check_specific_servers():
    """Check specific servers we know might exist"""
    print("\n🔍 Checking specific servers...")

    servers = [
        "@modelcontextprotocol/server-brave-search",
        "@modelcontextprotocol/server-google-search",
        "@modelcontextprotocol/server-perplexity",
        "@modelcontextprotocol/server-weather",
        "@modelcontextprotocol/server-openweathermap",
        "@modelcontextprotocol/server-weather-gov",
        "@modelcontextprotocol/server-weather-noaa",
        "@modelcontextprotocol/server-arxiv",
        "@modelcontextprotocol/server-filesystem",
        "@modelcontextprotocol/server-sqlite",
        "@modelcontextprotocol/server-postgres"
    ]

    available = []

    for server in servers:
        try:
            result = subprocess.run(
                ["npm", "view", server, "name"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✅ {server} - AVAILABLE")
                available.append(server)
            else:
                print(f"❌ {server} - NOT FOUND")
        except:
            print(f"❌ {server} - ERROR CHECKING")

    return available


def create_working_config(available_servers):
    """Create a working config based on available servers"""
    print("\n📝 Creating working config...")

    if not available_servers:
        print("⚠️ No servers found. Using fallback config.")
        config = {
            "mcpServers": {
                "placeholder": {
                    "command": "echo",
                    "args": ["No MCP servers available. Install one first."]
                }
            }
        }
    else:
        # Use the first available server
        first_server = available_servers[0]
        config = {
            "mcpServers": {
                "search": {
                    "command": "npx",
                    "args": ["-y", first_server]
                }
            }
        }

        print(f"✅ Using: {first_server}")

        # Add env vars if needed
        if "brave" in first_server:
            config["mcpServers"]["search"]["env"] = {
                "BRAVE_API_KEY": "${env:BRAVE_API_KEY}"
            }
        elif "perplexity" in first_server:
            config["mcpServers"]["search"]["env"] = {
                "PERPLEXITY_API_KEY": "${env:PERPLEXITY_API_KEY}"
            }
        elif "google" in first_server:
            config["mcpServers"]["search"]["env"] = {
                "GOOGLE_API_KEY": "${env:GOOGLE_API_KEY}",
                "GOOGLE_CSE_ID": "${env:GOOGLE_CSE_ID}"
            }

    # Save config
    with open("../working_mcp_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Config saved to 'working_mcp_config.json'")
    return config


def main():
    print("=" * 60)
    print("MCP Server Discovery Tool")
    print("=" * 60)

    # Search npm
    mcp_servers = search_npm_for_mcp()

    if not mcp_servers:
        print("\n⚠️ Couldn't search npm. Checking specific servers...")
        mcp_servers = check_specific_servers()

    # Create config
    config = create_working_config(mcp_servers)

    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS:")

    if mcp_servers:
        print(f"1. Install server: npm install -g {mcp_servers[0]}")
        print(f"2. Update your browser_mcp.json with the config above")
        print(f"3. Run: python app.py")

        # Get API key instructions
        if "brave" in mcp_servers[0]:
            print("\n🔑 Get Brave API key: https://brave.com/search/api/")
        elif "perplexity" in mcp_servers[0]:
            print("\n🔑 Get Perplexity API key: https://www.perplexity.ai/settings/api")
        elif "google" in mcp_servers[0]:
            print("\n🔑 Get Google API key: https://console.cloud.google.com/")
            print("   Need: Custom Search JSON API and Programmable Search Engine")
    else:
        print("No MCP servers found. Try manual installation:")
        print("\nOption A - Use Brave Search:")
        print("  npm install -g @modelcontextprotocol/server-brave-search")
        print("\nOption B - Use direct API calls (no MCP):")
        print("  See the DirectSearchAgent code below")

    print("=" * 60)


if __name__ == "__main__":
    main()