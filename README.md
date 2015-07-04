ProjectProfile
===================
A SublimeText 3 plugin, that allow to lock plugin non-related to current project type.
E.g. I have next plugins:

Common:
- Package Control
- STProjectMaker
- SublimeREPL

For Rust :
- Rust
- RustAutocomplete
- RustCodeFormatter

For arduino:
- Arduino-like IDE

I can create next ProjectProfile config:

    {
    	"always": ["Package Control", "0_package_control_loader", "STProjectMaker", "bz2", "ssl-linux", "SublimeREPL"],
    	"profiles": {
    		"rust": {
    			"packages": ["Rust", "RustAutocomplete", "RustCodeFormatter"]
    		},
    		"arduino": {
    			"packages": ["Arduino-like IDE"]
    		}
    	}
    }

And add next to Rust project:
    {
    "profile": "rust",
    }

P.S. Some plugins can't be locked before restart.