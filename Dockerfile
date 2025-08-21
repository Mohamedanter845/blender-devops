FROM blenderkit/headless-blender:blender-4.4

WORKDIR /app


COPY blender /app/blender
COPY textures /app/textures
RUN mkdir -p /app/output

# Command  Blender headless
CMD ["/home/headless/blender/blender", "-b", "-P", "/app/blender/auto_scene.py"]


