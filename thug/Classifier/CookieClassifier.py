#!/usr/bin/env python
#
# CookieClassifier.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA

import logging
from .BaseClassifier import BaseClassifier

log = logging.getLogger("Thug")


class CookieClassifier(BaseClassifier):
    default_rule_file   = "rules/cookieclassifier.yar"
    default_filter_file = "rules/cookiefilter.yar"
    classifier          = "Cookie Classifier"

    def __init__(self):
        BaseClassifier.__init__(self)

    def classify(self, url, cookie):
        for match in self.rules.match(data = cookie):
            if (url, match) in self.matches:
                continue

            self.matches.append((url, match))

            if self.discard_url_match(url, match): # pragma: no cover
                continue

            self.handle_match_etags(match)

            rule = match.rule
            meta = match.meta
            tags = ",".join([" ".join(t.split('_')) for t in match.tags])
            log.ThugLogging.log_classifier("cookie", url, rule, tags, meta)

        for c in self.custom_classifiers:
            self.custom_classifiers[c](url, cookie)

    def filter(self, url, cookie):
        ret = False

        for match in self.filters.match(data = cookie):
            rule = match.rule
            meta = match.meta
            tags = ", ".join([" ".join(t.split('_')) for t in match.tags])
            log.ThugLogging.log_classifier("cookiefilter", url, rule, tags, meta)
            ret = True

        return ret
