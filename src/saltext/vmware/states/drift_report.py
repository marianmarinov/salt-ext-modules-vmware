# SPDX-License-Identifier: Apache-2.0
import logging

import saltext.vmware.utils.connect as connect
import saltext.vmware.states.esxi as esxi
import saltext.vmware.states.storage_policy as state_storage_policy

log = logging.getLogger(__name__)

__virtualname__ = "vmware_drift_report"


def __virtual__():
    return __virtualname__


def report(name, firewall_config, advanced_config, storage_policy):
    """
    Creates drift_report

    policies
        Policy list to set state to
    """

    firewall_result = __salt__[
        "vmware_esxi.firewall_config"](**firewall_config)
    advanced_result = __salt__[
        "vmware_esxi.advanced_config"](**advanced_config)
    storage_policy_result = __salt__["vsphere_storage_policy.storage_policy"](
        **storage_policy)

    esxi_result = {host: {"firewall_config": firewall_result[host],
                          "advanced_config": advanced_result[host]} for host in firewall_result}

    ret = {"name": name, "result": True, "comment": "",
           "changes": {"esxi": {esxi_result}, "storagePolicies": storage_policy_result}}
    return ret
