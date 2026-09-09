FROM oceanbase/seekdb:1.4.0-100000172026082615@sha256:00d7a1e22220d4bf12c8dacfb1bf5723e5cf5670078b1ce28b41015f4d833b18
RUN sed -i 's|/var/lib/oceanbase|/var/lib/seekdb|g; s|seekdb_systemd_start 2>/dev/null$|seekdb_systemd_start 2>/dev/null \&|' /root/start.sh
