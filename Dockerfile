# AI2THOR Task Planner - CPU Docker Image
# Supports X11 forwarding for display output

# =============================================================================
# Stage 1: Build/Download dependencies
# =============================================================================
FROM python:3.12-slim-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install gdown for Google Drive downloads and ai2thor for pre-download
RUN pip install --no-cache-dir gdown ai2thor==4.2.0

# Download pretrained models
WORKDIR /downloads
RUN mkdir -p pretrained_models \
    && gdown --folder "https://drive.google.com/drive/folders/1UjADpBeBOMUKXQt-qSULIP3vM90zr_MR" -O pretrained_models/

# Pre-download ai2thor builds (without X11 requirement)
RUN python -c "\
import os; \
import ai2thor._builds; \
from ai2thor.build import Build; \
from ai2thor.platform import Linux64; \
releases_dir = os.path.join(os.path.expanduser('~'), '.ai2thor', 'releases'); \
os.makedirs(releases_dir, exist_ok=True); \
b = Build(Linux64, ai2thor._builds.COMMIT_ID, False, releases_dir); \
b.download(); \
print('AI2THOR build downloaded to', b.base_dir)"

# =============================================================================
# Stage 2: Final runtime image
# =============================================================================
FROM python:3.12-slim-bookworm

LABEL maintainer="AI2THOR Task Planner"
LABEL description="Task execution on iTHOR simulator using PDDL planning and OGAMUS"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # X11 and display
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxrandr2 \
    libxcursor1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxinerama1 \
    x11-utils \
    # OpenGL and rendering
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libegl1-mesa \
    libglu1-mesa \
    libvulkan1 \
    mesa-vulkan-drivers \
    # Audio (required by Unity)
    libasound2 \
    libpulse0 \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copy project files
COPY . .

# Copy pretrained models from builder stage
COPY --from=builder /downloads/pretrained_models/ /app/Utils/pretrained_models/

# Copy pre-downloaded ai2thor builds from builder stage
COPY --from=builder /root/.ai2thor/ /root/.ai2thor/

# Ensure the pre-compiled FF planner binary is executable
RUN chmod +x /app/OGAMUS/Plan/PDDL/Planners/FF/ff

# Create required directories
RUN mkdir -p images pddl/problems pddl/outputs Results

# Set environment variables for X11 forwarding
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Default command
CMD ["python", "main.py"]
