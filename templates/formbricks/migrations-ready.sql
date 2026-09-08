SELECT EXISTS (
  SELECT 1 FROM public.railway_template_migrations
  WHERE component = 'formbricks' AND release = :'release'
);
