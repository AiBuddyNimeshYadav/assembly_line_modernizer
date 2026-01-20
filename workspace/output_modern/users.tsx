import React, { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Dialog } from 'primereact/dialog';
import { Panel } from 'primereact/panel';
import { Toolbar } from 'primereact/toolbar';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { Toast } from 'primereact/toast';
import { PrimeReactProvider } from 'primereact/api';
import axios from 'axios';
import 'primereact/resources/themes/lara-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

interface User {
    id: number | null;
    name: string;
    email: string;
    createdDate: string;
}

const UserManagement: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const [selectedUser, setSelectedUser] = useState<User | null>(null);
    const [displayDialog, setDisplayDialog] = useState<boolean>(false);
    const [dialogMode, setDialogMode] = useState<'create' | 'edit'>('create');
    const toast = useRef<Toast>(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async (term: string = '') => {
        try {
            const response = await axios.get<User[]>(`/api/users`, {
                params: { searchTerm: term }
            });
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users:', error);
            toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Failed to fetch users', life: 3000 });
        }
    };

    const handleSearchSubmit = () => {
        fetchUsers(searchTerm);
    };

    const handleNewUserClick = () => {
        setSelectedUser({ id: null, name: '', email: '', createdDate: new Date().toISOString() });
        setDialogMode('create');
        setDisplayDialog(true);
    };

    const handleEditUserClick = (user: User) => {
        setSelectedUser({ ...user }); // Clone user to avoid direct state modification
        setDialogMode('edit');
        setDisplayDialog(true);
    };

    const handleDeleteUser = async (user: User) => {
        confirmDialog({
            message: `Are you sure you want to delete user "${user.name}"?`,
            header: 'Confirmation',
            icon: 'pi pi-exclamation-triangle',
            accept: async () => {
                try {
                    await axios.delete(`/api/users/${user.id}`);
                    toast.current?.show({ severity: 'success', summary: 'Success', detail: 'User deleted successfully', life: 3000 });
                    fetchUsers(searchTerm); // Refresh the table
                } catch (error) {
                    console.error('Error deleting user:', error);
                    toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Failed to delete user', life: 3000 });
                }
            },
            reject: () => {
                // Do nothing on reject
            }
        });
    };

    const handleSaveUser = async () => {
        if (!selectedUser || !selectedUser.name || !selectedUser.email) {
            toast.current?.show({ severity: 'warn', summary: 'Validation', detail: 'Name and Email are required', life: 3000 });
            return;
        }

        try {
            if (dialogMode === 'create') {
                await axios.post('/api/users', selectedUser);
                toast.current?.show({ severity: 'success', summary: 'Success', detail: 'User created successfully', life: 3000 });
            } else {
                await axios.put(`/api/users/${selectedUser.id}`, selectedUser);
                toast.current?.show({ severity: 'success', summary: 'Success', detail: 'User updated successfully', life: 3000 });
            }
            setDisplayDialog(false);
            setSelectedUser(null);
            fetchUsers(searchTerm); // Refresh the table
        } catch (error) {
            console.error('Error saving user:', error);
            toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Failed to save user', life: 3000 });
        }
    };

    const handleCancelDialog = () => {
        setDisplayDialog(false);
        setSelectedUser(null);
    };

    const handleDialogInputChange = (field: keyof User, value: string) => {
        setSelectedUser((prevUser) => (prevUser ? { ...prevUser, [field]: value } : null));
    };

    const dateBodyTemplate = (rowData: User) => {
        return new Date(rowData.createdDate).toLocaleDateString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
        });
    };

    const actionBodyTemplate = (rowData: User) => {
        return (
            <div className="flex gap-2">
                <Button icon="pi pi-pencil" className="p-button-rounded p-button-text" onClick={() => handleEditUserClick(rowData)} />
                <Button icon="pi pi-trash" className="p-button-rounded p-button-text p-button-danger" onClick={() => handleDeleteUser(rowData)} />
            </div>
        );
    };

    const toolbarLeftContents = (
        <React.Fragment>
            <InputText
                id="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search users..."
                className="mr-2"
            />
            <Button label="Search" icon="pi pi-search" onClick={handleSearchSubmit} />
        </React.Fragment>
    );

    const toolbarRightContents = (
        <React.Fragment>
            <Button label="New User" icon="pi pi-plus" onClick={handleNewUserClick} />
        </React.Fragment>
    );

    const dialogFooter = (
        <div className="flex justify-content-end gap-2">
            <Button label="Cancel" icon="pi pi-times" onClick={handleCancelDialog} className="p-button-secondary" />
            <Button label="Save" icon="pi pi-check" onClick={handleSaveUser} />
        </div>
    );

    return (
        <PrimeReactProvider>
            <Toast ref={toast} />
            <ConfirmDialog />
            <div className="user-management-container p-4">
                <Panel header="User Management" className="user-panel">
                    <Toolbar start={toolbarLeftContents} end={toolbarRightContents} className="mb-4" />

                    <DataTable
                        id="userTable"
                        value={users}
                        paginator
                        rows={10}
                        selectionMode="single"
                        selection={selectedUser}
                        onSelectionChange={(e) => setSelectedUser(e.value)}
                        dataKey="id"
                        emptyMessage="No users found."
                    >
                        <Column field="id" header="ID" sortable />
                        <Column field="name" header="Name" sortable />
                        <Column field="email" header="Email" sortable />
                        <Column field="createdDate" header="Created Date" body={dateBodyTemplate} sortable />
                        <Column header="Actions" body={actionBodyTemplate} style={{ width: '10rem' }} />
                    </DataTable>
                </Panel>

                <Dialog
                    id="userDialog"
                    header={dialogMode === 'create' ? 'New User Details' : 'Edit User Details'}
                    visible={displayDialog}
                    modal
                    onHide={handleCancelDialog}
                    footer={dialogFooter}
                    style={{ width: '30vw' }}
                >
                    {selectedUser && (
                        <div className="p-fluid formgrid grid">
                            <div className="field col-12">
                                <label htmlFor="name">Name:</label>
                                <InputText
                                    id="name"
                                    value={selectedUser.name}
                                    onChange={(e) => handleDialogInputChange('name', e.target.value)}
                                    required
                                    autoFocus
                                    className={!selectedUser.name ? 'p-invalid' : ''}
                                />
                            </div>
                            <div className="field col-12">
                                <label htmlFor="email">Email:</label>
                                <InputText
                                    id="email"
                                    value={selectedUser.email}
                                    onChange={(e) => handleDialogInputChange('email', e.target.value)}
                                    required
                                    className={!selectedUser.email ? 'p-invalid' : ''}
                                />
                            </div>
                        </div>
                    )}
                </Dialog>
            </div>
        </PrimeReactProvider>
    );
};

export default UserManagement;