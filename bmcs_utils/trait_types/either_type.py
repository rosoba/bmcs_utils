#-------------------------------------------------------------------------
#
# Copyright (c) 2009, IMB, RWTH Aachen.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in simvisage/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.simvisage.com/licenses/BSD.txt
#
# Thanks for using Simvisage open source!
#
# Created on Aug 7, 2009 by: rchx

from traits.api import TraitType, HasTraits, TraitError, Dict
from traitsui.api import View, Item
from bmcs_utils.editors import EitherTypeEditor

class EitherType(TraitType):
    editor_factory = EitherTypeEditor

    # TODO - initialization still not correct.
    def __init__(self, default_value=None, options = [], **metadata):
        # validate that these are trait types
        self.default_value, _ = options[0]
        self.options_dict = {key: value for key, value in options}
        metadata.update({'options': options})
        super(EitherType, self).__init__(**metadata)
        self._cached_objects = {}

    def validate(self, object, name, key):
        ''' Set the trait value '''
        klass = self.options_dict.get(key,None)
        if klass == None:
            raise TraitError('type %s not in the type scope' % klass)
        # check if the last instance of the klass has been
        # registered earlier in the trait history
        object = self._cached_objects.get(key,None)
        if object:
            new_value = object
        else:
            new_value = klass()
            self._cached_objects[key] = new_value
        # attach the key to the trait instance
        # editor uses it to asociate the value with the option.
        new_value._key = key
        return new_value

    def get_default_value(self):
        '''Take the first class to construct the value'''
        _, klass = self.options[0]
        value = klass()
        return (0, value)

