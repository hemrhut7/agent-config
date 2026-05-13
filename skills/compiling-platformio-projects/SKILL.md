---
name: compiling-platformio-projects
description: "Use PlatformIO (PIO) to compile and build embedded development projects. Trigger when the user requests compiling code, running a build, running pio run, or handling .ino/.cpp hardware projects."
---
# PlatformIO Compilation Skill

This skill is responsible for executing the build process of PlatformIO projects and ensuring the build artifacts are correctly generated.

## Core Workflow

1. **Environment Verification**: Check if the `platformio.ini` configuration file exists in the current directory.
2. **Execute Compilation**: Run the `pio run` command.
3. **Result Analysis**:
   - If the compilation is successful, confirm the binary files generated in the `.pio/build/` directory.
   - If the compilation fails, analyze the terminal output and refer to [TROUBLESHOOTING.md](TROUBLESHOOTING.md) to make corrections.

## Common Commands

### Execute Standard Compilation

```bash
pio run
```

### Clean and Recompile

```bash
pio run -t clean
pio run
```

### Compile for Specific Environment (if multiple exist)

```bash
# Assuming the environment name is esp32dev
pio run -e esp32dev
```

## Notes

- **Path Specification**: Always use forward slashes `/` when handling project paths.
- **Dependencies**: If missing libraries are prompted, prioritize checking the `lib_deps` setting.
- **Feedback Loop**: If the compilation fails, correct the code or configuration and re-execute step 2 until verification passes.
