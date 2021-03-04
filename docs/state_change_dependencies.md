
# Introduce dependencies between state variables

Assume two model components defined as follows

```python
import bmcs_utils.api as bu
import traits.api as tr


class M1(bu.Model):
    length = bu.Float(10, GEO=True)


class M2(bu.Model):
    m1 = tr.Instance(M1, ())

    a = tr.Property(depends_on='+GEO')

    @tr.cached_property
    def _get_a(self):
        return self.m1.length ** 2

```
to ensure a consistent state of the model
in a running application model traits are 
categorized using the tags specifying 
the kind of information that the model parameter
delivers. Following tags are predefined
```
GEO, BC, DSC, ALG, INT, TIME
```
When defining derived properties of the model 
components, these tags are used to handle 
the changes upwards in the hierarchy.

The model tree structure is extracted by 
traversing the base classes. Each subclass
of `InteractiveModel` contains the events 
`_TAG` which can be included in the local 
definition of properties and observers 
in the local class definition. 