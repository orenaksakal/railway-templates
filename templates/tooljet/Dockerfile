FROM tooljet/tooljet-ce:v3.20.223-lts@sha256:63ce8a302f3ecc47be3f9bc4e6adf0e34c3b61e7071d216523623fa5b529ac31
COPY --chmod=755 templates/tooljet/start.sh /app/railway-start.sh
ENTRYPOINT ["/app/railway-start.sh"]
CMD ["npm", "run", "start:prod"]
