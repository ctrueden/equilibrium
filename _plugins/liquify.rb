# Renders Liquid within a string, e.g. the content of another page that has
# not been rendered yet.
#
# Note: Stock GitHub Pages does not run custom plugins. That is OK, since this
# filter is only used to embed GM pages, which exist only in local builds.
module Jekyll
  module LiquifyFilter
    def liquify(input)
      Liquid::Template.parse(input.to_s).render!(@context)
    end
  end
end

Liquid::Template.register_filter(Jekyll::LiquifyFilter)
