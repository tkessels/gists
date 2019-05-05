#!/bin/bash
docker build --no-cache -t tabledevil/sep:latest -f sep_dev.dockerfile  .
tag=$(docker run -it tabledevil/sep:latest version | grep -Pio "(?<=Dockertag: )[\d._]+" )
echo "NEW TAG : ${tag}"
docker tag tabledevil/sep tabledevil/sep:${tag}
docker push "tabledevil/sep:${tag}"
docker push "tabledevil/sep:latest"
