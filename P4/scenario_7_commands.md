# Scenario 7: Docker Export / Import vs Save / Load Reference Guide

This scenario covers the Docker commands for saving/loading images and exporting/importing containers.

---

## 1. `docker save` & `docker load` (Image Level)

- **Purpose:** Archives a **Docker Image** to a `.tar` file, including all its layers, history, tags, and metadata.
- **Use Case:** Sharing images between air-gapped systems or backing up full images without a registry.

### Commands:

```bash
# 1. Save an image to a tar archive
docker save -o iris-webapp-image.tar iris-webapp:s1

# 2. View archive details (optional)
ls -lh iris-webapp-image.tar

# 3. Load the image back into Docker
docker load -i iris-webapp-image.tar

# 4. Verify loaded image
docker images
```

---

## 2. `docker export` & `docker import` (Container Level)

- **Purpose:** Exports a **running or stopped container's filesystem** to a flattened `.tar` file.
- **Use Case:** Creating a clean, lightweight baseline snapshot without intermediate image layers or history.

### Commands:

```bash
# 1. Export a container's filesystem to a tar file
docker export -o iris-container-fs.tar webcnt_cmp_vol

# 2. View archive size (optional)
ls -lh iris-container-fs.tar

# 3. Import the filesystem tar archive as a new image
cat iris-container-fs.tar | docker import - iris-imported:latest

# 4. Verify imported image
docker images iris-imported
```

---

## 📊 Key Differences Cheat Sheet

| Feature | `docker save` / `docker load` | `docker export` / `docker import` |
| :--- | :--- | :--- |
| **Operates On** | **Images** | **Containers** |
| **History & Layers** | Preserved (all layer history intact) | Flattened (single new layer, history stripped) |
| **Metadata & CMD** | Preserved (`ENTRYPOINT`, `ENV`, `CMD`) | Lost (must be re-specified if running) |
| **Primary Goal** | Perfect backup/transfer of existing images | Creating a base image from container snapshot |
