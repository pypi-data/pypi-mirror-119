RUN DEBIAN__FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
    glmark2 \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libgles2 \
    libvulkan1 \
    libvulkan-dev \
    vulkan-utils \
    && rm -rf /var/lib/apt/lists/* && \
    VULKAN_API_VERSION=`dpkg -s libvulkan1 | grep -oP 'Version: [0-9|\.]+' | grep -oP '[0-9|\.]+'` && \
    mkdir -p /etc/vulkan/icd.d/ && \
    echo \
   "{\
        \"file_format_version\" : \"1.0.0\",\
        \"ICD\": {\
            \"library_path\": \"libGLX_nvidia.so.0\",\
            \"api_version\" : \"${VULKAN_API_VERSION}\"\
        }\
    }" > /etc/vulkan/icd.d/nvidia_icd.json    

# needed?
COPY --from=glvnd /usr/share/glvnd/egl_vendor.d/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json

ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics,display,video,utility,compute
