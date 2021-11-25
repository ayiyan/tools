
CEPH_NODES="pool1-ert-lab-ceph-1    pool1-ert-lab-ceph-2    pool1-ert-lab-ceph-3"


#########################  Test Data #######################
# CEPH_NODES="pool1-ert-lab-ceph-1    pool1-ert-lab-ceph-2" #
# CEPH_NODES_K8S="k8s-node1 k8s-node2"                      #
############################################################

ccdinfo(){
   echo "[$2|5]Info>> " $1
}

remote_command(){
   ssh eccd@"$2" "sudo su - root -c  '$1'"
}


#Step-1
res=`kubectl get nodes -o wide | awk  'BEGIN{count=0} {if (NR>1 && $2 != "Ready"){ count=count+1}; if(NR>1){ printf  "%-30s%-15s\n",$1,$6 > "node_info"}} END{ print count }'`
[ $res -gt 0 ] && ccdinfo "cluster unhealthy" 1 && exit 
cat node_info  | sort -k 1n > template_node_info
ccdinfo "Finished" 1

#Step-2
array=(`kubectl get pv  | awk '{if(NR>1){printf "%s ",$1}}'`)

declare -a pv_array
declare -A pv_dict
number=0
for pv_name in ${array[@]}
do
	pv_info=`kubectl  describe  pv $pv_name | gawk '
	{
		if($1=="Labels:") server=$2;
		if($2=="ccd-local/by-path:") disk=$3;
		if($1=="ccd-local/partition-id:") partion=$2
	}
	END {
		printf "%s  %s  %s\n",server,disk,partion
	}'`

	pv_dict+=([${pv_name}]=${pv_info[@]})
done

for ceph_node in ${CEPH_NODES[@]}
do

	declare -A dict
	declare -a array_a
	declare -A temp_dict

	for key in $(echo ${!pv_dict[*]})
	do
		arrary=(${pv_dict[$key][@]})
		worker_node=`echo ${arrary[0]} |awk -F "=" '{print $NF}'`
		disk=`echo ${arrary[1]} |awk -F "/" '{print $NF}'`
		partion_num=`echo ${arrary[2]}`
		if [ $worker_node == $ceph_node ]; 
		then
			if [[ ${!temp_dict[*]} =~ $disk ]];
			then
				partion=${temp_dict[$disk]}
				drive=$partion$partion_num
				array_a[$num]=$drive
			else
				partion=`remote_command  "ls -l /dev/disk/by-path/|grep $disk| grep [a-z]$" $ceph_node` 
				partion=`echo $partion| awk -F "/" '{print $NF}'`
				temp_dict+=([${disk}]=$partion)
				drive=$partion$partion_num
				array_a[$num]=$drive				
			fi
			let num=num+1
		fi
	done
	value=`echo ${array_a[@]}`
	ccdinfo "There are ${#array_a[@]} pv in the $ceph_node server," 2
	ccdinfo "Used partion [$value] in the $ceph_node server " 2
	dict+=([${ceph_node}]=${array_a[@]})
	unset array_a
done

res=`kubectl get pods -n  local-storage  -o wide 2>/dev/null | awk  'BEGIN{count=0} {if (NR>1 && $3 != "Running") count=count+1;if(NR>1){printf "%-30s%-15s\n",$7,$1 >"pod_info"} } END{ print count }'`
[ $res -ne 0 ] && ccdinfo "local storage abnormal" 2 && exit
cat pod_info  | sort -k 1n > template_pod_info
join -a2 template_node_info template_pod_info  |awk 'BEGIN{printf "%-30s%-30s%-30s\n","node_name","node_ip","pod_name";}{printf "%-30s%-30s%-30s\n",$1,$2,$3}' > pod_info
kubectl cordon $CEPH_NODES >> /dev/null
# kubectl cordon $CEPH_NODES_K8S >> /dev/null
rm template_pod_info
rm template_node_info
ccdinfo "Finished" 2 

#Step-3
pv_bound_num=`kubectl get pv 2>/dev/null | awk  'BEGIN{count=0} {if (NR>1 && $5 == "Bound") count=count+1 } END{ print count }'`
[ $pv_bound_num -gt 0 ] && ccdinfo "pvxx.pvxx， still in bound" 3 && exit
total_pv_num=`kubectl  get pv 2>/dev/null | wc -l`
kubectl get pv 2>/dev/null | awk  '{if (NR>1) system("kubectl delete pv "$1) }' >> /dev/null

pv_bound_num=`kubectl  get pv 2>/dev/null | wc -l`
[ $pv_bound_num -eq 0 ] &&  ccdinfo "PV delelted successfully" 3 || (ccdinfo "pvxx still exists" 3 && exit)


# Step-4
for node in ${CEPH_NODES[@]}
do
	block_dev_b=`remote_command "lsblk | grep sdb | wc -l" $node`
	let block_dev_b=$block_dev_b-1
	ccdinfo "get ${block_dev_b} partions of Sdb Disks in the $node server " 4

	block_dev_c=`remote_command "lsblk | grep sdc | wc -l" $node`
	let block_dev_c=$block_dev_c-1
	ccdinfo "get ${block_dev_c} partions of Sdc Disks in the $node server" 4
done

ccdinfo "umount partions" 4

for key in $(echo ${!dict[*]})
do
        for drive in ${dict[$key]}
        do
   			remote_command "umount /dev/$drive 2&>1" $key
        done
        remote_command "dd if=/dev/zero of=/dev/sdb bs=1M count=1024 >>/dev/null 2>&1 " $key
		remote_command "dd if=/dev/zero of=/dev/sdc bs=1M count=1024 >>/dev/null 2>&1" $key
done

ccdinfo "Finished umount operation" 4

ccdinfo "Finished dd operation" 4

for node in ${CEPH_NODES[@]}
do
	block_dev_b=`remote_command "lsblk | grep sdb | wc -l" $node`
	let block_dev_b=$block_dev_b-1
	ccdinfo "get ${block_dev_b} partions of Sdb Disk in the $node server" 4
	[ $block_dev_b -eq 1 ] && ccdinfo "sdb  partition cleard"

	block_dev_c=`remote_command  "lsblk | grep sdc | wc -l" $node`
	let block_dev_c=$block_dev_c-1
	ccdinfo "get ${block_dev_c} partions of Sdc Disk in the $node server" 4
	[ $block_dev_c -eq 1 ] && ccdinfo "sdc  partition cleard"
done

#Step-5
ccdinfo "remove pod of local-storage" 5
for i in `kubectl get pods -n local-storage | awk 'NR != 1 {print $1}'`; do kubectl delete pod $i -n local-storage >> /dev/null; done
ccdinfo "Finished remove pod operation" 5

pv=`kubectl  get pv 2>/dev/null | wc -l`
ccdinfo "Waiting for the PV to be created" 5

while [ $pv -ne $total_pv_num ]
do
  pv=`kubectl  get pv 2>/dev/null | wc -l`
  sleep 10s
done
ccdinfo "pv numer is ready" 5
kubectl uncordon $CEPH_NODES >>/dev/null
# kubectl uncordon $CEPH_NODES_K8S >>/dev/null
ccdinfo "PV recreated successfully" 5